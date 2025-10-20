'use client';
import { useState } from 'react';
import { useAccount, useWriteContract, useSimulateContract } from 'wagmi';
import { nftABI } from '../lib/nftABI';
import dynamic from 'next/dynamic';

const NFT_ADDR = '0xYour721DeployedOnMumbai'; // deploy once (see step 3)

const Visualiser = dynamic(() => import('./Visualiser'), { ssr: false });

export default function MintCard() {
  const { address } = useAccount();
  const [file, setFile] = useState<File | null>(null);
  const [ipfsHash, setIpfsHash] = useState<string>('');
  const [isUploading, setIsUploading] = useState(false);

  const uploadToIpfs = async () => {
    if (!file) return;
    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${process.env.NEXT_PUBLIC_PINATA_JWT}`,
        },
        body: formData,
      });
      const data = await res.json();
      setIpfsHash(data.IpfsHash);
    } catch (error) {
      console.error('Error uploading to IPFS:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const { data: config } = useSimulateContract({
    address: NFT_ADDR,
    abi: nftABI,
    functionName: 'mint',
    args: [ipfsHash],
    enabled: !!ipfsHash,
  });

  const { write } = useWriteContract();

  return (
    <div className="mt-8 space-y-4">
      <input type="file" accept="audio/mpeg" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={uploadToIpfs} disabled={isUploading || !file} className="px-4 py-2 bg-pink-600 rounded disabled:bg-gray-500">
        {isUploading ? 'Uploading...' : 'Upload to IPFS'}
      </button>
      {ipfsHash && (
        <>
          <p className="text-sm">IPFS hash: {ipfsHash}</p>
          <button onClick={() => write(config?.request)} disabled={!write} className="px-4 py-2 bg-purple-600 rounded disabled:bg-gray-500">
            Mint WAV NFT
          </button>
          <Visualiser hash={ipfsHash} />
        </>
      )}
    </div>
  );
}

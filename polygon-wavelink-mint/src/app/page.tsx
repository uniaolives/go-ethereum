'use client';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import MintCard from '../components/MintCard';
import { Providers } from './providers';

export default function Home() {
  return (
    <Providers>
      <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center">
        <ConnectButton />
        <MintCard />
      </main>
    </Providers>
  );
}

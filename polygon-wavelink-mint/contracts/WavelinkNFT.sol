//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
contract WavelinkNFT is ERC721 {
    uint public nextId = 1;
    constructor() ERC721("Wavelink","WV"){}
    function mint(string calldata ipfsHash) external returns(uint id){
        id = nextId++;
        _safeMint(msg.sender, id);
        _setTokenURI(id, string.concat("ipfs://",ipfsHash));
    }
}

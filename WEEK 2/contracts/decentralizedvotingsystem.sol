// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DecentralizedVoting {
    
    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }

    struct Voter {
        bool isRegistered;
        bool hasVoted;
        uint256 votedCandidateId;
    }

    address public admin;
    uint256 public candidateCount;
    
    mapping(uint256 => Candidate) public candidates;
    mapping(address => Voter) public voters;

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this function");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function addCandidate(string memory _name) public onlyAdmin {
        candidateCount++;
        candidates[candidateCount] = Candidate(candidateCount, _name, 0);
    }

    function registerVoter(address _voterAddress) public onlyAdmin {
        require(!voters[_voterAddress].isRegistered, "Voter is already registered");
        voters[_voterAddress].isRegistered = true;
    }

    function vote(uint256 _candidateId) public {
        Voter storage sender = voters[msg.sender];
        require(sender.isRegistered, "You are not registered to vote");
        require(!sender.hasVoted, "You have already voted");
        require(_candidateId > 0 && _candidateId <= candidateCount, "Invalid candidate ID");

        sender.hasVoted = true;
        sender.votedCandidateId = _candidateId;
        candidates[_candidateId].voteCount++;
    }

    // Dynamic Winner Tally Scanner as required by DecodeLabs instructions
    function winningProposal() public view returns (uint256 winningCandidateId, string memory winningName) {
        uint256 highestVoteCount = 0;
        
        for (uint256 i = 1; i <= candidateCount; i++) {
            if (candidates[i].voteCount > highestVoteCount) {
                highestVoteCount = candidates[i].voteCount;
                winningCandidateId = candidates[i].id;
                winningName = candidates[i].name;
            }
        }
    }
}
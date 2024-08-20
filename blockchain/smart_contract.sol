pragma solidity ^0.8.0;

contract InsuranceClaim {
    struct Claim {
        uint id;
        string policyState;
        string incidentType;
        uint totalClaimAmount;
        bool processed;
    }

    mapping(uint => Claim) public claims;
    uint public claimCount = 0;

    function createClaim(string memory _policyState, string memory _incidentType, uint _totalClaimAmount) public {
        claimCount++;
        claims[claimCount] = Claim(claimCount, _policyState, _incidentType, _totalClaimAmount, false);
    }

    function processClaim(uint _id) public {
        Claim storage claim = claims[_id];
        claim.processed = true;
    }
}

// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract EHRTimestamping {
    struct MedicalRecord {
        uint256 timestamp;
        string patientId;
        bytes32 recordHash;
    }

    mapping(string => MedicalRecord) public records;

    event RecordTimestamped(bytes32 recordHash, uint256 timestamp, string patientId);

    function timestampRecord(bytes32 recordHash, string memory patientId) public {
        require(bytes(records[patientId].patientId).length == 0, "Record already exists for this patientId");

        MedicalRecord memory record = MedicalRecord({
            timestamp: block.timestamp,
            recordHash: recordHash,
            patientId: patientId
        });

        records[patientId] = record;

        emit RecordTimestamped(recordHash, block.timestamp, patientId);
    }

    function getRecord(string memory patientId) public view returns (MedicalRecord memory) {
        return records[patientId];
    }
}
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract HealthRecords {
    // Struct to represent a health record
    struct Record {
        string patientId; // Patient ID
        string socialSecurityNumber;
        string patientName; // Patient name
        string dateOfAdmission; // Date of admission
        string dateOfBirth; // Date of birth
        string gender; // Gender
        string contactNumber; // Contact number
        string insurerName; // Insurer name
        uint256 timestamp; // Timestamp when the record was added
        address owner; // Address of the owner who added the record
    }

    // Mapping to store records by their unique identifiers
    mapping(string => Record) public records;

    // Array to store record keys for iteration
    string[] public recordKeys;

    // Event emitted when a new record is added
    event RecordAdded(
        string indexed recordId,
        string patientId,
        string socialSecurityNumber,
        string patientName,
        string dateOfAdmission,
        string dateOfBirth,
        string gender,
        string contactNumber,
        string insurerName,
        uint256 timestamp,
        address owner
    );

    // Function to add a new health record
    function addRecord(
        string memory patientId,
        string memory socialSecurityNumber,
        string memory patientName,
        string memory dateOfAdmission,
        string memory dateOfBirth,
        string memory gender,
        string memory contactNumber,
        string memory insurerName
    ) public {
        require(bytes(patientId).length > 0,
         "Patient ID must not be empty");
        require(
            bytes(socialSecurityNumber).length > 0,
            "SocialSecurityNumber must not be empty"
        );
        require(
            bytes(patientName).length > 0,
            "Patient name must not be empty"
        );
        require(
            bytes(dateOfAdmission).length > 0,
            "Date of admission must not be empty"
        );
        require(
            bytes(dateOfBirth).length > 0,
            "Date of birth must not be empty"
        );
        require(bytes(gender).length > 0, "Gender must not be empty");
        require(
            bytes(contactNumber).length > 0,
            "Contact number must not be empty"
        );
        require(
            bytes(insurerName).length > 0,
            "Insurer name must not be empty"
        );

        // Generate a unique record ID based on patient ID and patient name
        string memory recordId = generateRecordId(patientId, patientName);

        require(
            bytes(records[recordId].patientId).length == 0,
            "Record ID already exists"
        );

        // Get the current timestamp and the address of the sender
        uint256 timestamp = block.timestamp;
        address owner = msg.sender;

        records[recordId] = Record(
            patientId,
            socialSecurityNumber,
            patientName,
            dateOfAdmission,
            dateOfBirth,
            gender,
            contactNumber,
            insurerName,
            timestamp,
            owner
        );
        recordKeys.push(recordId); // Add record key to array
        emit RecordAdded(
            recordId,
            patientId,
            socialSecurityNumber,
            patientName,
            dateOfAdmission,
            dateOfBirth,
            gender,
            contactNumber,
            insurerName,
            timestamp,
            owner
        );
    }

    // Function to check if a record exists
    function recordExists(string memory recordId) public view returns (bool) {
        return (bytes(records[recordId].patientId).length > 0);
    }

    // Function to retrieve a record using patient ID
    function getRecordByPatientId(string memory patientId)
        public
        view
        returns (
            string memory recordId,
            string memory socialSecurityNumber,
            string memory patientName,
            string memory dateOfAdmission,
            string memory dateOfBirth,
            string memory gender,
            string memory contactNumber,
            string memory insurerName,
            uint256 timestamp,
            address owner
        )
    {
        for (uint256 i = 0; i < recordKeys.length; i++) {
            string memory key = recordKeys[i];
            if (
                keccak256(bytes(records[key].patientId)) ==
                keccak256(bytes(patientId))
            ) {
                return (
                    key,
                    records[key].socialSecurityNumber,
                    records[key].patientName,
                    records[key].dateOfAdmission,
                    records[key].dateOfBirth,
                    records[key].gender,
                    records[key].contactNumber,
                    records[key].insurerName,
                    records[key].timestamp,
                    records[key].owner
                );
            }
        }
        revert("Record not found for the given patient ID");
    }

    // Internal function to generate a unique record ID
    function generateRecordId(
        string memory patientId,
        string memory patientName
    ) internal pure returns (string memory) {
        return string(abi.encodePacked(patientId, "-", patientName));
    }
}

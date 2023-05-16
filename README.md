# Datalogger Sanitizer

Sanitize the CSV file to be more optimal to analyze data.

## Configuration

- ```n_bytes```: Number of bytes on each CAN frame
- ```n_ids_max```: Number of IDs on the raw CSV - counting with blanks!!!
- ```n_ids```: Number of used IDs
- ```structure```: Structure of the CAN frames
  - ```can_id```: CAN ID 
  - ```vars```: Variables defined in this frame. Mind the byte order.
    - ```name```: Textual description of the variable
    - ```length```: Number of bytes allocated to this variable
    - ```values```: Keep this array empty, it is used by the script

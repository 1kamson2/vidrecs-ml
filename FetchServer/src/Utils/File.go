package Utils

import "os"

func FileReader(filePath string) []byte {
	/*
		Read files.

		Arguments:
			filePath: a path to a file to be read.

		Returns:
			File content in bytes.
	*/

	if data, err := os.ReadFile(filePath); err == nil {
		return data
	}

	return []byte{}
}

func FileWriter(filePath, fileContent string) (err error) {
	/*
		Write content to a file.

		Arguments:
			filePath: a path to a file to be written to.
			fileContent: content of a file.

		Returns:
			Error if it occurred while writing to a file, otherwise `nil`.
	*/

	panic("Method not implemented")
	return nil
}

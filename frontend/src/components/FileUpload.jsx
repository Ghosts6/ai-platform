import React from 'react';
import { FiUpload, FiFile } from 'react-icons/fi';

const FileUpload = ({ onFileChange, selectedFile }) => {
  return (
    <div className="flex items-center gap-3 p-4 border-t border-primary/20 bg-surface/30">
      <input
        type="file"
        id="file-upload"
        onChange={onFileChange}
        className="hidden"
      />
      <label
        htmlFor="file-upload"
        className="flex items-center gap-2 px-4 py-2 bg-secondary/30 text-accent rounded-lg cursor-pointer hover:bg-secondary/50 transition-colors duration-300"
      >
        <FiUpload className="w-4 h-4" />
        <span>Choose File</span>
      </label>
      {selectedFile && (
        <div className="flex items-center gap-2 text-sm text-accent/70">
          <FiFile className="w-4 h-4" />
          <span>{selectedFile.name}</span>
        </div>
      )}
    </div>
  );
};

export default FileUpload;

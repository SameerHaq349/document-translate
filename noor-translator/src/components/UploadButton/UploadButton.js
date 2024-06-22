import React, {useState} from 'react'
import './UploadButton.css'



const UploadButton = (props) => {

    const handleUpload = (event) => {
        props.setFileTwo(event.target.files[0]);
        console.log("hi",event.target.files)
      

        
    };

    return (
        <div className="upload-button">
            
            <input type="file" className="input" id="file" onChange={handleUpload}></input>
            <label for="file" className="input-label">Choose a file</label>
        
        </div>
    )
}

export default UploadButton


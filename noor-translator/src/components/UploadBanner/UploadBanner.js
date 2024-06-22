import './UploadBanner.css'
import React from 'react'
import UploadButton from '../UploadButton/UploadButton'


const UploadBanner = (props) => {
    return (
        <div className='upload-banner'>
            <div className='logo'>
                    <img src='/logo.png' width='175px'></img>
            </div>
            <div className='translate-ppt'>
                Translate PowerPoint
            </div>
            <div className='sub-text'>
                Drag and drop a PowerPoint file here to translate it to a language of your choice
            </div>
            <div>
                <UploadButton setFileTwo={props.setFileOne}></UploadButton>
            </div>
        </div>
    )
}


export default UploadBanner

import React from 'react'
import './TranslatedQueue.css'
import Card from '../Card/Card' 

const Queue = (props) => {
    return (
        <div>
            <div className='queue-title'>
                Translated Documents
            </div>
            {props.loadingCard==false ? <div className='default-queue-message'>No Files in Queue</div> : <Card name={props.file.name + "_" + props.language} size={props.file.size} setFileTwo={props.setFileOne} downloadLink={props.fileDownloadLink} downloadButton={props.downloadButtonAppear} isDownload={true}></Card>}
           
          
            
        </div>
    )
}

export default Queue 
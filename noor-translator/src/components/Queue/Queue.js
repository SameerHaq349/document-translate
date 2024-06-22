import React from 'react'
import './Queue.css'
import Card from '../Card/Card' 

const Queue = (props) => {
    return (
        <div>
            <div className='queue-title'>
                Queue
            </div>
            {props.file==null ? <div className='default-queue-message'>No Files in Queue</div> : <Card name={props.file.name} size={props.file.size} setFileTwo={props.setFileOne}></Card>}
           
          
            
        </div>
    )
}

export default Queue 
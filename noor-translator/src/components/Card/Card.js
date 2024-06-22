import React, {useState} from 'react'
import './Card.css'



const Card = (props) => {

    const [cancelButton, setCancelButton] = useState(false)

    let file_size = 0
    if (props.size > 999999999) {
        file_size = Math.trunc(props.size/1000000000).toString() + " GB"

    }
    else if (props.size > 999999) {
        file_size = Math.trunc(props.size/1000000).toString() + " MB"
    }
    else if (props.size > 999) {
        file_size = Math.trunc(props.size/1000).toString() + " KB"
    }
    else {
        file_size = props.size + " Bytes"
    }

    const handleMouseEnter = () => {
        setCancelButton(true)
    }

    const handleMouseExit = () => {
        setCancelButton(false)
    }

    const cancelSelection = () => {
        props.setFileTwo(null)
    }

    return (
        <div className='card' onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseExit}>
            <div className='card-container'>
                <div className='card-container-left'>
                    <img src="/Frame.png" width="7%"></img>
                    <div className='file-name-container'>
                        <div className='file-title'>
                            {props.name}
                        </div>
                        <div className='file-size'>
                            {file_size}
                        </div>
                    </div>
                </div>
                {props.downloadButton==true ?  < a href={"https://" + props.downloadLink} className='x'><img src="/Vector.png" className="download-image" ></img></a>:(cancelButton==true ? <div className='x' onClick={cancelSelection}>x</div> : <div></div>)}
                
            </div>
        </div>
    )
}

export default Card
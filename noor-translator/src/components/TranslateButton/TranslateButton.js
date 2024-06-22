import React from 'react'
import './TranslateButton.css'

const TranslateButton = (props) => {
    return (
        <button onClick={props.onClick} type="button" className='button-template'>
            <div className='button-text'>
                Translate
            </div>
        </button>
    )
}

export default TranslateButton
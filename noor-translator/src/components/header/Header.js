import React from 'react'
import './Header.css'

const Header = () => {
    return (
        <div className='Header'>
            <div className='Logo'>
                <img src={'/earth_2_line.png'} alt='earth' width="20px"></img>
                <div className="global-translate">Global Translate</div>
            </div>
        </div>
    )
}

export default Header
import React, {useState, useEffect} from 'react'
import './LanguageSelector.css'

const LanguageSelector = (props) => {
    const [languageArray, setLanguageArray] = useState([])
    

    useEffect(() => {
        const fetchLanguages = async () => {

            try {
                const url = 'http://127.0.0.1:5000/languages';
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setLanguageArray(data);  
            } catch (error) {
                console.error('Error fetching languages:', error)
            }
        
        }

        fetchLanguages()
    }, []);

    const handleLanguageSelection = (event) => {
        props.setLanguageCode(event.target.value)
        console.log(event.target.value)

        props.setLanguage(event.target.selectedOptions[0].getAttribute('languageName'))

    }

    

    return (
        <div className='language-selector'>
            <div className='translate-label'>
                Translate to:
            </div>
            <select className="language-selection" name="language" id="language" onChange={handleLanguageSelection}>
                    <option key="none" value="none" selected disabled hidden>Select a language</option>
                {languageArray.map((x) => (
                    <option languageName={x.name} key={x.name} value={x.language}> {x.name} </option>
                ))}
                </select>
        </div>
    )
}


export default LanguageSelector
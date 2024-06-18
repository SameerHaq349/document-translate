import React, { useState, useEffect } from 'react';
import './FileUpload.css';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [buttonAppear, setButtonAppear] = useState(false);
    const [downloadLink, setDownloadLink] = useState('')
    const [languageArray, setLanguageArray] = useState([])
    const [languageCode, setLanguageCode] = useState('')
    const [language, setLanguage] = useState('')

    
        useEffect(() => {
            const fetchLanguages = async () => {

                try {
                    const url = 'https://slidetranslate-smashbyz2q-uc.a.run.app/languages';
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




    
   
    const handleUpload = (event) => {
        setFile(event.target.files[0]);
    };

    const handleClick = async () => {
        const url = 'https://slidetranslate-smashbyz2q-uc.a.run.app';
        const formData = new FormData();
        formData.append('file', file);
        formData.append('languageCode', languageCode)
        formData.append('language', language)

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            }).then(resp => resp.json())
            .then(data => downloadButton(data.link));
            
            
            
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    const downloadButton = (link) => {
        setButtonAppear(true)
        setDownloadLink(link)
    }

    const handleLanguageSelection = (event) => {
        setLanguageCode(event.target.value)
        console.log(event.target.value)

        setLanguage(event.target.getAttribute("key"))

    }


    return (
        <div>
            <div className="select-file">
                <div className="file-drop">
                    <input className="input" type="file" onChange={handleUpload}></input>
                </div>
            </div>
            <div>
                {buttonAppear ? <a href={"https://" + downloadLink}>download now</a>:<button onClick={handleClick}>Translate</button> }
                <select name="language" id="language" onChange={handleLanguageSelection}>
                    <option key="none" value="none" selected disabled hidden>Select a language</option>
                {languageArray.map((x) => (
                    <option key={x.name} value={x.language}> {x.name} </option>
                ))}
                </select>
            </div>
            
        </div>
    );
};

export default FileUpload;

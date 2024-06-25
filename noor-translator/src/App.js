import FileUpload from './components/FileUpload';
import Header from './components/header/Header'
import UploadBanner from './components/UploadBanner/UploadBanner.js';
import Queue from './components/Queue/Queue.js';
import LanguageSelector from './components/LanguageSelector/LanguageSelector.js';
import TranslateButton from './components/TranslateButton/TranslateButton.js';
import UploadButton from './components/UploadButton/UploadButton.js';
import TranslatedQueue from './components/TranslatedQueue/TranslatedQueue.js'
import './App.css';
import React, {useState} from 'react'

function App() {

  const [file, setFile] = useState(null);
  const [languageCode, setLanguageCode] = useState('')
  const [language, setLanguage] = useState('')
  const [LoadingCard, setLoadingCard] = useState(false)
  const [downloadLink, setDownloadLink] = useState('')
  const [buttonAppear, setButtonAppear] = useState(false);

  const handleClick = async () => {
    console.log(language)
    console.log(file)
    setLoadingCard(true)
    const url = 'http://localhost:8080';
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

const printHi = () => {
  console.log("hello")
}

  

  
  return (
    <div className="App">
      <div className="border">
        <Header></Header>
        <UploadBanner setFileOne={setFile}></UploadBanner>
        <Queue setFileOne={setFile} file={file}></Queue>
        <div className="button-container">
          <LanguageSelector language={language} setLanguage={setLanguage} languageCode={languageCode} setLanguageCode={setLanguageCode}></LanguageSelector>
          <TranslateButton onClick={handleClick}></TranslateButton>
        </div>
        <TranslatedQueue file={file} downloadButtonAppear={buttonAppear} fileDownloadLink={downloadLink} loadingCard={LoadingCard} language={language}></TranslatedQueue>
      </div>
    </div>
  );
}

export default App;


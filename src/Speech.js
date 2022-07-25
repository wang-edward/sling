import React, { useState, useEffect } from "react";
import { useSpeechSynthesis } from "react-speech-kit";
const Speech = () => {
  const text = 'apple is a fruit'
  let index = 1;
  const [value, setValue] = useState("");
  const { speak } = useSpeechSynthesis();

  useEffect(() => {
        const interval = setInterval(() => {
            console.log('This will run after 1 second!')
              setValue(text.substring(0, index))
              index+=1;
              console.log(index);
              if(index>text.length) {
                  clearInterval(interval)
              }
              speak({ text: text.substring(index - 2, index - 1) });
          }, 3000);
          const timer = setTimeout(() => {
              speak({ text: text });
              setValue(text);
            }, 3000 * text.length + 1000);
            
          
    return () => {clearTimeout(timer);};
  }, []);

  return (
    <div className="speech">
      <div className="group">
        <h1>Sling</h1>
        <h5>Translated characters:</h5>
        <input id="inputText" onChange={(e) => setValue(e.target.value)} value={ value }/>
      </div>
      <div className="group">
        <button onClick={() => speak({ text: value })}>
          Speech
        </button>
      </div>
    </div>
    );
};
export default Speech;



//start time = getTime()
// current_time = getTime()

// if(current_time - start_time > 5) {
//     //code
//     start_time = current_time

// }
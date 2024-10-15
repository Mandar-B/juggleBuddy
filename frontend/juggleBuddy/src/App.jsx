import React, { useState } from 'react';
import axios from 'axios';
import './App.css';  

const VideoFeed = () => {
    const [videoStarted, setVideoStarted] = useState(false);

    const startVideo = async () => {
        try {
            await axios.post('http://127.0.0.1:5000/start_video');
            setVideoStarted(true);
        } catch (error) {
            console.error("Error starting video:", error);
        }
    };

    const stopVideo = async () => {
        try {
            //await axios.post('http://127.0.0.1:5000/stop_video');
            //setVideoStarted(false);
            window.location.reload();

        } catch (error) {
            console.error("Error stopping video:", error);
        }
    };

    return (
        <div className='my-div'>
          <h1>JuggleBuddy!</h1>
            <h3>Start Tracking</h3>
            {!videoStarted && <button onClick={startVideo}>Start Video</button>}
            {videoStarted && (
                <>
                    <button onClick={stopVideo}>Stop Video</button>
                    <img
                        src="http://127.0.0.1:5000/video_feed"
                        alt="Video Feed"
                        style={{ width: '640px', height: '480px' }}
                    />
                </>
            )}
        </div>
    );
};

export default VideoFeed;

import React from 'react';

const VideoFeed = () => {
    return (
        <div>
            <h2>Live Juggling Tracker</h2>
            <img
                src="http://127.0.0.1:5000/video_feed"
                alt="Video Feed"
                style={{ width: '640px', height: '400px' }}
            />
        </div>
    );
};

export default VideoFeed;

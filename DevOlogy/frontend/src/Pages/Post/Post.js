import React, { useState, useEffect } from 'react';


function Post(props) {
    const [image, setImage] = useState(props.imagePath)
    const [likes, setLikes] = useState({})
    const [comments, setComments] = useState({})
    const [requestUserHasLiked, setRequestUserHasLiked] = useState({})
    useEffect(() => {
        return () => {
            
        }
    }, [])
    return (
        <div className="post">
            
        </div>
    )
}

export default Post


import React, { useState, useEffect } from "react";
import "./Post.css";
import ReactReadMoreReadLess from "react-read-more-read-less";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faHeart,
  faComment,
  faBookmark,
} from "@fortawesome/free-regular-svg-icons";
import {
  faHeart as faHeartFilled,
  faBookmark as faBookmarkFilled,
} from "@fortawesome/free-solid-svg-icons";
import { asyncFetchRequest, fetchRequest } from "../../../helpers/fetchRequest";

function Post(props) {
  const [likes, setLikes] = useState(0);
  const [comments, setComments] = useState({});
  const [requestUserHasLiked, setRequestUserHasLiked] = useState(false);
  const [requestUserHasBookmarked, setRequestUserHasBookmarked] =
    useState(false);
  const knowRequestUserHasLiked = async () => {
    fetchRequest({
      path_: "/api/knowIfPostWasLiked/",
      method: "POST",
      body: { custom_id: props.postData.custom_id },
      next: (data) => {
        setRequestUserHasLiked(data.response);
      },
    });
  };
  const knowRequestUserHasBookmarked = async () => {
    fetchRequest({
      path_: "/api/knowIfPostWasBookmarked/",
      method: "POST",
      body: { custom_id: props.postData.custom_id },
      next: (data) => {
        setRequestUserHasBookmarked(data.response);
      },
    });
  };
  const getPostLikes = async () => {
    fetchRequest({
      path_: "/api/getPostLikes/",
      method: "POST",
      body: { custom_id: props.postData.custom_id },
      next: (data) => {
        setLikes(data.response);
      },
    });
  };
  const toggleLike = () => {
    if (requestUserHasLiked) {
      removeLike();
    } else {
      addLike();
    }
  };
  const toggleBookmark = () => {
    if (requestUserHasBookmarked) {
      removeBookmark();
    } else {
      addBookmark();
    }
  };
  const addLike = async () => {
    if (!requestUserHasLiked) {
      fetchRequest({
        path_: "/api/addLike/",
        method: "POST",
        body: { custom_id: props.postData.custom_id },
        next: (data) => {
          if (data.response === "Liked") {
            setRequestUserHasLiked(true);
            setLikes(likes + 1);
          }
        },
      });
    }
  };
  const removeLike = async () => {
    if (requestUserHasLiked) {
      fetchRequest({
        path_: "/api/removeLike/",
        method: "POST",
        body: { custom_id: props.postData.custom_id },
        next: (data) => {
          if (data.response === "Like Removed") {
            setRequestUserHasLiked(false);
            setLikes(likes - 1);
          }
        },
      });
    }
  };
  const addBookmark = async () => {
    if (!requestUserHasBookmarked) {
      fetchRequest({
        path_: "/api/addBookmark/",
        method: "POST",
        body: { custom_id: props.postData.custom_id },
        next: (data) => {
          if (data.response === "Bookmarked") {
            setRequestUserHasBookmarked(true);
          }
        },
      });
    }
  };
  const removeBookmark = async () => {
    if (requestUserHasBookmarked) {
      fetchRequest({
        path_: "/api/removeBookmark/",
        method: "POST",
        body: { custom_id: props.postData.custom_id },
        next: (data) => {
          if (data.response === "Bookmark Removed") {
            setRequestUserHasBookmarked(false);
          }
        },
      });
    }
  };
  useEffect(() => {
    knowRequestUserHasBookmarked();
    knowRequestUserHasLiked();
    getPostLikes();
  }, []);
  return (
    <div className="post my-2">
      <div className="container-fluid post-head py-1">
        <div className="post-dp">
          <a href={"/" + props.postData.username}>
            <img
              className="post-dp-img"
              src={props.postData.user_dp}
              alt={props.postData.username + "'s DP."}
            />
          </a>
        </div>
        <div className="post-head-username mx-2 my-1">
          <a className="link" href={"/" + props.postData.username}>
            {props.postData.username}
          </a>
        </div>
      </div>
      <div className="post-image">
        <img
          onDoubleClick={addLike}
          src={props.postData.picture}
          alt={
            props.postData.username +
            "'s post, posted on " +
            props.postData.posted_on
          }
        />
      </div>
      <div className="post-footer">
        <div className="container-fluid my-1 footer-icon-container">
          <div className="left">
            {requestUserHasLiked ? (
              <FontAwesomeIcon
                onClick={toggleLike}
                icon={faHeartFilled}
                color="red"
                size={"2x"}
                style={{ marginRight: "10px" }}
              />
            ) : (
              <FontAwesomeIcon
                onClick={toggleLike}
                icon={faHeart}
                color="black"
                size={"2x"}
                style={{ marginRight: "10px" }}
              />
            )}
            <FontAwesomeIcon icon={faComment} size={"2x"} />
            <p>{likes}</p>
          </div>
          <div className="right">
            {requestUserHasBookmarked ? (
              <FontAwesomeIcon
                icon={faBookmarkFilled}
                color="black"
                size={"2x"}
                onClick={toggleBookmark}
              />
            ) : (
              <FontAwesomeIcon
                onClick={toggleBookmark}
                icon={faBookmark}
                color="black"
                size={"2x"}
              />
            )}
          </div>
        </div>
        <div className="container-fluid">
          <a
            style={{ fontSize: "14px", marginLeft: "3px" }}
            className="link"
            href={"/" + props.postData.username}
          >
            <b>{props.postData.username}</b>
          </a>
          <div style={{ fontSize: "14px", marginLeft: "3px" }}>
            <ReactReadMoreReadLess
              charLimit={window.innerWidth > 700 ? 100 : 50}
              readMoreText={"Read More"}
              readLessText={"Read Less"}
            >
              {props.postData.caption}
            </ReactReadMoreReadLess>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Post;

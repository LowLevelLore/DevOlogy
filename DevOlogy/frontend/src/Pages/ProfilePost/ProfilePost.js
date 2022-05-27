import React, { Component } from "react";
import { faHeart as faHeartFilled } from "@fortawesome/free-solid-svg-icons";
import styles from "./ProfilePost.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { nFormatter } from "../../../helpers/numbers";

export default class ProfilePost extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isHovering: false,
    };
  }

  getHeight(id) {
    try {
      let element = document.getElementById(`post-${id}`);
      let height = element.clientHeight;
      return height;
    } catch {
      return 0;
    }
  }
  render() {
    return (
      <div
        className={styles.mainDiv}
        style={{
          height: this.state.isHovering
            ? this.getHeight(this.props.post.custom_id)
            : "auto",
        }}
      >
        <div
          id={`post-${this.props.post.custom_id}`}
          className={styles.post}
          onMouseEnter={() => {
            this.setState({ isHovering: true });
          }}
          onMouseLeave={() => {
            this.setState({ isHovering: false });
          }}
        >
          <a href={`/post/${this.props.post.custom_id}`}>
            <img
              src={this.props.post.picture}
              alt={`${this.props.post.user}'s post`}
            />
          </a>
        </div>
        {this.state.isHovering ? (
          <a href={`/post/${this.props.post.custom_id}`} style={{textDecoration: "none"}}>
          <div
            className={styles.hover}
            onMouseEnter={() => {
              this.setState({ isHovering: true });
            }}
            onMouseLeave={() => {
              this.setState({ isHovering: false });
            }}
            style={{
              top: -this.getHeight(this.props.post.custom_id),
              height: this.getHeight(this.props.post.custom_id),
            }}
          >
            <div style={{display: "flex", justifyContent: "center", alignItems: "center", flexDirection: "column"}}>
              <FontAwesomeIcon
                icon={faHeartFilled}
                color="white"
                style={{height: "auto", width: "22%"}}
              />
              <span style={{textDecoration: "none"}}>
                {nFormatter(this.props.post.likes)}
              </span>
            </div>
          </div>
          </a>
        ) : (
          <> </>
        )}
      </div>
    );
  }
}

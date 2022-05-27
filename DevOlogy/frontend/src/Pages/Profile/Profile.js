import React, { Component } from "react";
import "./Profile.css";
import Navbar from "../../components/Navbar/Navbar";
import { async } from "regenerator-runtime";
import { fetchRequest, syncFetchRequest } from "../../../helpers/fetchRequest";
import Button from "react-bootstrap/Button";
import { nFormatter } from "../../../helpers/numbers";
import ReactReadMoreReadLess from "react-read-more-read-less";
import splitArrayInX from "../../../helpers/splitInX";
import ProfilePost from "../ProfilePost/ProfilePost";

export default class Profile extends Component {
  constructor(props) {
    super(props);
    this.state = {
      requestUserData: {},
      ownProfile: false,
      biodata: {},
      posts: 0,
      followers: 0,
      following: 0,
      bio: "",
      links: [],
      profileUserData: {},
      page: 0,
      posts_objects: {},
    };
  }
  getprofileUserData = () => {
    console.log( window.location.pathname.split("/").reverse()[1])
    fetchRequest({
      path_: "/api/user/getProfileUserData/",
      method_: "POST",
      body: {username: window.location.pathname.split("/").reverse()[1]},
      next: (data) => {
        this.setState({profileUserData: data.response});
      }
    });
  }
  getUserBioData = () => {
    fetchRequest({
      path_: "/api/user/getBioData/",
      method: "POST",
      body: { username: window.location.pathname.split("/").reverse()[1] },
      next: (data) => {
        this.setState({
          bio: data.response.bio,
          links: data.response.bio_links,
        });
      },
    });
  };
  setRequestUserData = (data) => {
    this.setState({ requestUserData: data });
    this.compareIdFromUserName();
  };
  compareIdFromUserName = () => {
    syncFetchRequest({
      path_: "/api/user/getIdFromUserName/",
      method: "POST",
      body: { username: window.location.pathname.split("/").reverse()[1] },
      next: (data) => {
        if (data.status == 200) {
          if (data.response === this.state.requestUserData.id) {
            this.setState({ ownProfile: true });
          } else {
            this.setState({ ownProfile: false });
          }
        } else {
          window.location = "/";
        }
      },
    });
  };

  getFollowerFollowing = () => {
    fetchRequest({
      path_: "/api/user/getFollowerFollowing/",
      method: "POST",
      body: { username: window.location.pathname.split("/").reverse()[1] },
      next: (data) => {
        this.setState({
          posts: data.response.posts,
          followers: data.response.followers,
          following: data.response.following,
        });
      },
    });
  };

  getPosts = () => {
    fetchRequest({
      path_: "/api/user/getProfilePosts/",
      method: "POST",
      body: { username: window.location.pathname.split("/").reverse()[1] , page: this.state.page},
      next: (data) => {
        if (data.status == 200) {

          this.setState({
            posts_objects: {...this.state.posts_objects, ...data.data},
          });
          this.setState({
            page: this.state.page + 1,
          });
        }
      }
    });
  }

  UNSAFE_componentWillMount() {
    this.getUserBioData();
    this.getFollowerFollowing();
    this.getPosts();
  }

  componentDidMount(){
    this.getprofileUserData();
  }

  render() {
    return (
      <>
        <Navbar setUserData={this.setRequestUserData} />

        <div className="main-container">
          <div className="upperinfo">
            <div className="upperinfo-left">
              <div className="upperinfo-left-image">
                <img src={this.state.profileUserData.dp} alt="Your Dp" />
              </div>
            </div>
            <div className="upperinfo-right">
              <div className="uname">
                <div className="upperinfo-right-username">
                  <p>{this.state.profileUserData.username}</p>
                </div>
                {this.state.ownProfile ? (
                  <div className="upperinfo-right-edit">
                    <Button variant="outline-secondary" href="/editprofile">
                      {" "}
                      Edit Profile
                    </Button>
                  </div>
                ) : (
                  <div className="upperinfo-right-follow"></div>
                )}
              </div>
              <div className="followers-following">
                <p>{nFormatter(this.state.posts)} Posts </p>
                <p>{nFormatter(this.state.followers)} Followers</p>
                <p>{nFormatter(this.state.following)} Following</p>
              </div>
              <div className="bio top-right-bio">
                <p>
                  <ReactReadMoreReadLess
                    readMoreText={"Read More"}
                    readLessText={"Read Less"}
                  >
                    {this.state.bio}
                  </ReactReadMoreReadLess>
                </p>
                {this.state.links.length > 0 ? (
                  <div>
                    {this.state.links.map((link) => {
                      return (
                        <a
                          href={link.link}
                          key={link.id}
                          className="link-container"
                        >
                          <p
                            className="profile-bio-link"
                            style={{
                              textDecoration: "none",
                              fontSize: 14.5,
                              color: "rgb(35, 35, 255)",
                              width: "fit-content",
                            }}
                          >
                            {link.link}
                          </p>
                        </a>
                      );
                    })}
                  </div>
                ) : (
                  <> </>
                )}
              </div>
            </div>
          </div>
          <div className="bio centre-bio">
            <p>
              <ReactReadMoreReadLess
                readMoreText={"Read More"}
                readLessText={"Read Less"}
              >
                {this.state.bio}
              </ReactReadMoreReadLess>
            </p>
            {this.state.links.length > 0 ? (
              <div>
                {this.state.links.map((link) => {
                  return (
                    <a
                      href={link.link}
                      key={link.id}
                      className="link-container"
                    >
                      <p className="profile-bio-link" style={{textDecoration: "none",
                              fontSize: 13.5,
                              color: "rgb(35, 35, 255)",
                              width: "fit-content",}}>{link.link}</p>
                    </a>
                  );
                })}
              </div>
            ) : (
              <> </>
            )}
          </div>
          <div className="profile-posts-container">
              {splitArrayInX(Object.values(this.state.posts_objects), 3).map((arr) => {
                return (<div key={`${arr[0]}-${arr[1]}-${arr[2]}`} className="row-of-posts">
                    {arr.map((post) => {
                      return (
                        <ProfilePost post={post} key={post.custom_id}></ProfilePost>
                      )
                    })}
                </div>)
              })}
          </div>
        </div>
      </>
    );
  }
}

import React from 'react';
import './Header.css';
import headerLogo from  '../images/niv_logo7.png';

export default class Header extends React.Component {
    render() {
        return (
            <div id="logo-and-intro">
                <div id="logoDiv">
                    <img
                        src={headerLogo}
                        alt="NIV_Logo"
                        id="logo"
                    />
                </div>

                <div id="titleDiv">
                    <h1>The Network Infrastructure Visualizer</h1>
                </div>
                <div id="learnMoreDiv">
                    <a href="#introdiv" id="button">Learn more</a>
                </div>
            </div>
        );
    }

}
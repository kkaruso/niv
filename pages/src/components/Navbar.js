import React from 'react';
import './Navbar.css';

export default class Navbar extends React.Component {
    render() {
        return (
            <header>
                <ul class="navLinks">
                    <li><a href="#introduction">Über Uns</a></li>
                    <li><a href="#example">Beispiel</a></li>
                    <li><a href="#conclusion">Fazit</a></li>
                    <li><a href="#team">Team</a></li>
                </ul>
                <a class="getItNow" href="https://gitlab.rlp.net/top/21s/niv/niv/-/blob/dev/pages/public/introduction/introduction.md" target="_blank" rel="noreferrer">
                    <button>Installieren</button>
                </a>
            </header>
        );
    }
}
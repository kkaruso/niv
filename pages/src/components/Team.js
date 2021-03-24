import React from 'react';
import marcel_metzler from '../images/marcel_metzler.png';
import enis_kecevic from '../images/enis_kecevic.png';
import tim_thomas from '../images/tim_thomas.png';
import daniel_grosmayer from '../images/daniel_grosmayer.png';
import darwin_schulz from '../images/darwin_schulz.png';
import musa_tek from '../images/musa_tek.jpg';
import gulbarchyn_akbekova from '../images/gulbarchyn_akbekova.png';
import mohamad_said_himmat from '../images/mohamad_said_himmat.png';
import mohamed_salim_guezguez from '../images/mohamed_salim_guezguez.png';
import './Team.css';

export default class Team extends React.Component {
    render() {
        return (
            <div id="teamDiv">
                <h2>Das Team</h2>
                <div class="teamColumn">
                    <div class="card">
                        <img src={marcel_metzler} alt="Marcel_Metzler" class="member" />
                        <div class="container">
                            <h2>Marcel Metzler</h2>
                            <p class="title">Product Owner</p>
                        </div>
                    </div>
                </div>

                <div class="teamColumn">
                    <div class="card">
                        <img src={enis_kecevic} alt="Enis_Kecevic" class="member" />
                        <div class="container">
                            <h2>Enis Kecevic</h2>
                            <p class="title">Scrum Master</p>
                        </div>
                    </div>
                </div>
                <div class="teamColumn">
                    <div class="card">
                        <img src={tim_thomas} alt="Tim_Thomas" class="member" />
                        <div class="container">
                            <h2>Tim Thomas</h2>
                            <p class="title">Developer</p>
                        </div>
                    </div>
                </div>
                <div class="teamColumn">
                    <div class="card">
                        <img src={daniel_grosmayer} alt="Daniel_Grosmayer" class="member" />
                        <div class="container">
                            <h2>Daniel Grosmayer</h2>
                            <p class="title">Developer</p>
                        </div>
                    </div>
                </div>
                <div class="teamColumn">
                    <div class="card">
                        <img src={darwin_schulz} alt="Darwin_Schulz" class="member" />
                        <div class="container">
                            <h2>Darwin Schulz</h2>
                            <p class="title">Developer</p>
                        </div>
                    </div>
                </div>
                <div class="teamColumn">
                    <div class="card">
                        <img src={musa_tek} alt="Musa_Tek" class="member" />
                        <div class="container">
                            <h2>Musa Tek</h2>
                            <p class="title">Developer</p>
                        </div>
                    </div>
                </div>
                <div class="teamColumn">
                    <div class="card">
                        <img src={gulbarchyn_akbekova} alt="Gulbarchyn_Akbekova" class="member" />
                        <div class="container">
                            <h2>Gulbarchyn Akbekova</h2>
                            <p class="title">Developer</p>
                        </div>
                    </div>
                </div>
                <div class="teamColumn">
                    <div class="card">
                        <img src={mohamad_said_himmat} alt="Mohamad_Said_Himmat" class="member" />
                        <div class="container">
                            <h2>Mohamad-Said Himmat</h2>
                            <p class="title">Developer</p>
                        </div>
                    </div>
                </div>
                <div class="teamColumn">
                    <div class="card">
                        <img src={mohamed_salim_guezguez} alt="Mohamed_Salim_Guezguez" class="member" />
                        <div class="container">
                            <h2>Mohamed-Salim Guezguez</h2>
                            <p class="title">Developer</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
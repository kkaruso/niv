import React from 'react'
import Navbar from './Navbar';
import Header from './Header';
import Intro from './Intro';
import Example from './Example';
import Conclusion from './Conclusion';
import PosterAndSlider from './PosterAndSlider';
import Team from './Team';
import Footer from './Footer';
import './App.css';

export default class App extends React.Component {
  render() {
    return (
      <div>
        <Navbar />
        <Header />
        <Intro />
        <Example />
        <Conclusion />
        <PosterAndSlider />
        <Team />
        <Footer />
      </div>
    );
  }
}
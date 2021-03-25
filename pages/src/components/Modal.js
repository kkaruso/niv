import React from "react";
import exampleOne from '../images/example1_code.png'
import exampleTwo from '../images/example2_command.png'
import exampleThree from '../images/example3_diagramm.png'
import "./Modal.css";

const Modal = (props) => {
  const divStyle = {
    display: props.displayModal ? "block" : "none",
  };
  function closeModal(e) {
    e.stopPropagation();
    props.closeModal();
  }

  function getImage(imageNumber) {
    if (imageNumber === 1) {
        return exampleOne
    } else if (imageNumber === 2) {
        return exampleTwo
    } else {
        return exampleThree
    }
  }
  return (
    <div className="modal" onClick={closeModal} style={divStyle}>
      <div className="modalContent" onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={closeModal}>
          &times;
        </span>
        <img className="modalImage" src={getImage(props.imageNumber)} alt="" />
      </div>
    </div>
  );
};
export default Modal;

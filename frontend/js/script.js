function eventHandler(event) {
  console.log("Button clicked!");
  imgSwap("assets/placeholder_dwa.jpg");
  console.log(event);
}

function imgSwap(new_img) {
  let front_img = document.getElementById("first-buffer");
  let back_img = document.getElementById("second-buffer");
  back_img.src = new_img;
  back_img.onload = function() {
    let front_img_copy = front_img;
    front_img = back_img;
    front_img.id = "first-buffer";
    back_img = front_img_copy;
    back_img.id = "second-buffer";
  };
}

const buttons = document.querySelectorAll(".action-button");
console.log(buttons);
buttons.forEach((button) => button.addEventListener("click", eventHandler));

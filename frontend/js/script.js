// TODO: Add config parser
// TODO: Need to refresh the page which is bad
async function eventHandler(event) {
  console.log(`[INFO] Button clicked:\n${event.target}`);
  const button = event.target;
  // sanitize here
  let json2send = JSON.stringify({
    sender: "me",
    action: button.id,
  });
  console.log(json2send);
  const response = await fetch("http://127.0.0.1:8888", {
    method: "POST",
    body: json2send,
    headers: {
      "Content-Type": "application/json",
      connection: "close",
    },
  });
  console.log(response);
  imgSwap("assets/placeholder_dwa.jpg");
}

function imgSwap(new_img) {
  const front_img = document.getElementById("first-buffer");
  const tempImg = new Image();
  tempImg.onload = () => {
    front_img.src = new_img;
  };
  tempImg.src = new_img;
}

const buttons = document.querySelectorAll(".action-button");
buttons.forEach((button) => button.addEventListener("click", eventHandler));

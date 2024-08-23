const form = document.querySelector('form');
form.addEventListener('submit', callData);

let uploadedFile;
async function previewImage(event) {
  const file = event.target.files[0];
  uploadedFile = file;
  const preview = document.getElementById('image-preview');
  const fileUpload = document.getElementById('upload-file');
  // const noSelect = document.getElementById('no-select');
  const scanningLine = document.getElementById('scanning-line');
  const overlay = document.getElementById('overlay');

  if (file) {
    const reader = new FileReader();
    reader.onload = async function (e) {
      preview.src = e.target.result;
      preview.style.display = 'block';
      fileUpload.style.display = "none";
      // noSelect.style.display = "none";
      scanningLine.style.display = 'block';
      overlay.style.display = 'flex';
    }
    reader.readAsDataURL(file);
    await callData()
  }
}

async function callData(event) {
  document.getElementById('no_detected').style.display = "none";
  const scanningLine = document.getElementById('scanning-line');
  const overlay = document.getElementById('overlay');
  let term_plans = ['aditya_birla_digishield_plans', 'bajaj_alliance_life_etouch', 'hdfc_click2protect_super', 'icici_iprotect_smart', 'max_life_smart_secure_plus']
  let health_plans = ['aditya_birla_activ_health', 'bajaj_alliance_health_guard', 'hdfc_ergo', 'icici_lombard', 'tata_aig']
  try {
    const formData = new FormData();
    formData.append('file', uploadedFile);
    const response = await fetch('http://74.225.136.211:5000/insurance', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    console.log('Success:', data);
    scanningLine.style.display = 'none';
    overlay.style.display = 'none';
    if (data.error == 'no detections were made.') {
      console.log("HERE");
      document.getElementById('no_detected').style.display = "flex";
    } else if (data.term_plan_bool == 1 && data.logo != 'NA') {
      let index = term_plans.indexOf(data.logo);
      document.getElementById(data.logo + '_detected').style.display = "flex";
      document.getElementById('hr_tag').style.display = "block";
      document.getElementById('suggestions').style.display = "flex";
      document.getElementById('detected').style.display = "flex";
      if (index !== -1) {
        term_plans.splice(index, 1);
      }
      console.log(term_plans);
      for (let i of term_plans) {
        document.getElementById(i).style.display = "flex"
      }
    } else if (data.health_plan_bool == 1 && data.logo != 'NA') {
      let index = health_plans.indexOf(data.logo);
      document.getElementById(data.logo + '_detected').style.display = "flex";
      document.getElementById('hr_tag').style.display = "block";
      document.getElementById('suggestions').style.display = "flex";
      document.getElementById('detected').style.display = "flex";
      if (index !== -1) {
        health_plans.splice(index, 1);
      }
      console.log(health_plans);
      for (let i of health_plans) {

        document.getElementById(i).style.display = "flex"
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

async function login() {
  try {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    const response = await fetch('http://74.225.136.211:5000/login', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        password
      })
    });
    const data = await response.json();
    console.log('Success:', data);
    if (data.status == 'false') {
      document.getElementById('wrong_creds').style.display = "block";
    } else {
      window.location.href = "http://74.225.136.211/main.html";
    }
  } catch (error) {
    console.error('Error:', error);
  }
}
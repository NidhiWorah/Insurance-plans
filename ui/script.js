const form = document.querySelector('form');
form.addEventListener('submit', callData);

let uploadedFile;
async function previewImage(event) {
  const file = event.target.files[0];
  uploadedFile = file;
  const preview = document.getElementById('image-preview');
  const fileUpload = document.getElementById('upload-file');
  const noSelect = document.getElementById('no-select');
  const scanningLine = document.getElementById('scanning-line');
  const overlay = document.getElementById('overlay');

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      preview.src = e.target.result;
      preview.style.display = 'block';
      fileUpload.style.display = "none";
      noSelect.style.display = "none";
      scanningLine.style.display = 'block';
      overlay.style.display = 'flex';
    }
    reader.readAsDataURL(file);
  }
}

async function callData(event) {
  const scanningLine = document.getElementById('scanning-line');
  const overlay = document.getElementById('overlay');
  let term_plans = ['aditya_birla_digishield_plans', 'bajaj_alliance_life_etouch', 'hdfc_click2protect_super', 'icici_iprotect_smart', 'max_life_smart_secure_plus']
  let health_plans = ['aditya_birla_activ_health', 'bajaj_alliance_health_guard', 'hdfc_ergo', 'icici_lombard', 'tata_aig']
  try {
    const formData = new FormData();
    formData.append('file', uploadedFile);
    const response = await fetch('http://localhost:5000/insurance', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    console.log('Success:', data);
    scanningLine.style.display = 'none';
    overlay.style.display = 'none';
    if (data.term_plan_bool == 1) {
      let index = term_plans.indexOf(data.logo);

      if (index !== -1) {
        term_plans.splice(index, 1);
      }
      console.log(term_plans);
      for (let i of term_plans) {
        document.getElementById(i).style.display = "flex"
      }
    } else if (data.health_plan_bool == 1) {
      let index = health_plans.indexOf(data.logo);

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
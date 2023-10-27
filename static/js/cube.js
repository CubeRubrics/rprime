/*!
 * This file is part of the CubeRubrics project 
 *
 * Copyright 2023 The Cube Rubrics Authors (https://github.com/CubeRubrics)
 * Licenseed under the GNU Affero GPL (https://raw.githubusercontent.com/CubeRubrics/rprime/main/LICENSE)
 */

var cube_config = {
    spinners: 0,
    messages: 0,
    api_timeout_delay: 1500,
};


function clear_hash() {
    console.log('Clearing hash');
    history.pushState("", document.title, window.location.pathname + window.location.search);
}


function load_bs_extras() {
    console.log('bs extras: start');
    // enable tooltips everywhere 
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // show toasts
    let toastElList = [].slice.call(document.querySelectorAll('.toast'))
    let toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl)
    })
    toastList.forEach(toast => toast.show())

    console.log('bs extras: end');
}


function get_spinner(color = '', size = '') {
    cube_config.spinners++;
    console.log('Making spinner #', cube_config.spinners, color)

    let s = document.getElementById('generic-spinner').cloneNode(true)
    s.id = s.id.concat('-').concat(cube_config.spinners)
    s.dataset.spinner = cube_config.spinners

    if (color != '') {
      let c = 'text-'.concat(color)
      s.classList.add(c)
    }

    if (size != '') {
        let z = 'spinner-border-'.concat(size)
        s.classList.add(z);
    }
    console.log('Spinner #', cube_config.spinners, ': ', s)
    return s;
}


function subscription_modal() {
    // Subscription modal
    let subsEl = document.getElementById('subscriptionModal')
    subsEl.addEventListener('hide.bs.modal', function (event) {
      clear_hash();
    })

    subsEl.addEventListener('show.bs.modal', function (event) {
      window.location.hash = "subscribe";
    })

    var subsModal = new bootstrap.Modal(subsEl, {
      backdrop: 'static'
    })
    return subsModal;
}


function load_modals() {
    let modals = {
        subscription: subscription_modal(),
    };

    console.log(modals);
    return modals;
}


// Whole section on processing a form
//
// TODO: should probably turn these all into a class for forms since they are 
// all passing around this form element as "f"

function remove_input_feedback(t) {
    console.log('Input on ', t, '\m ... removing feedback')
    t.classList.remove('is-invalid')
    t.classList.remove('is-valid')
    if (t.message_ids) {
        for (let i=0; i<t.message_ids.length; i++) {
            console.log('Removing feedback message: ', t.message_ids[i])
            document.getElementById(t.message_ids[i]).remove();
        }
        t.message_ids = []
    }
}

function notate_api_form_errs(f) {
    let errs = f.errors || []

    for (let i=0; i<errs.length; i++) {
        let err = errs[i];
        if (err.elem && err.msg) {
            console.log('Error #', i, ': ', err.msg)
            // set a removal first
            if (err.elem.tagName == 'INPUT' || err.elem.tagname == 'TEXTAREA')
                err.elem.onkeyup = (event) => {remove_input_feedback(event.srcElement)};
            else
                err.elem.onchange = (event) => {remove_input_feedback(event.srcElement)};

            err.elem.dataset.baseClass = err.elem.className
            err.elem.classList.add('is-invalid')
            err.elem.dataset.apiFeedbackTagged = true

            cube_config.messages++;
            let emsg = document.createElement('small')
            emsg.id = 'feedback-msg-'.concat(cube_config.messages)
            emsg.className = 'invalid-feedback text-end text-capitalize'
            emsg.innerHTML = err.msg
            emsg.dataset.apiFeedback = true
            if (!err.elem.message_ids) 
                err.elem.message_ids = [emsg.id, ];
            else 
                err.elem.message_ids.push(emsg.id);
            err.elem.after(emsg)

        }
        else {
            console.error('Error list element ', i, ' lacks elem and/or msg: ', err)
        }
    }
}


function api_form_process(f) {
    console.log('Processing form: ', f)
    let dat = {}
    f.errors = []

    for (let i=0; i<f.length; i++) {
        let e = f[i]
        console.log('Checking field ', e)

        switch (e.tagName) {
            default:
                if (e.value && e.name) {
                    if (e.hasAttribute('required') && !e.value) {
                        f.errors.push({
                            elem: e,
                            msg: 'required',
                        })
                    }
                    else {
                        // get the second element, allowing for a prefix and postfix
                        let k = e.name.split('-')[1]

                        let v = e.value.trim()
                        if (e.hasAttribute('maxlength'))
                            v = v.substr(0, e.maxlength)
                        dat[k] = v;
                    }
                }
        }
        //console.log('Element ', i, e, '\n- ', e.name, e.value)
    }

    notate_api_form_errs(f)
    return dat;
}


function unlock_form(s, f) {
    s.disabled = false
    s.className = s.dataset.baseClass

    if (s.spinner) {
        s.spinner.remove()
    }

    s.title = s.dataset.initTitle
    f.title = f.dataset.initTitle

    s.innerHTML = s.dataset.baseHTML

    let inputs = f.elements

    for (let i=0; i<inputs.length; i++) {
        if (inputs[i].dataset.readOnly == 'true') {
            inputs[i].setAttribute('readonly', true)
        }
        else {
            inputs[i].removeAttribute('readonly')
        }
    }

    f.dataset.apiLocked = false;
    s.dataset.apiLocked = false;
    return 0;
}


function lock_form(s, f) {
    // s = the 'submitter' on the event
    // f = the form element
    if (f.dataset.apiLocked == "true") {
        throw new Error('Cannot lock a form already in processing!');
    }

    else {
        console.log('Locking form ', f)
        // do any cleanup I know of...
        let fe = f.querySelectorAll('[data-api-feedback="true"]')
        for (let i=0; i<fe.length; i++) {
            console.log('Removing ', i, ' api message: ', fe[i])
            fe[i].remove()
        }

        // FIXME: There is a bootstrap.js way to do this 
        fe = f.querySelectorAll('[data-api-feedback-tagged="true"]')
        for (let i=0; i<fe.length; i++) {
            let fi = fe[i]
            fe[i].classList.remove('invalid-feedback')
            fe[i].classList.remove('valid-feedback')
        }
    }
    // lock the button
    s.disabled = true
    s.dataset.baseClass = s.className
    s.dataset.baseHTML = s.innerHTML
    s.innerHTML = '';
    s.classList.add('disabled')

    s.dataset.apiLocked = true;
    f.dataset.apiLocked = true;
    f.dataset.initTitle = f.title
    f.title = 'Locked while processing'
    s.dataset.initTitle = s.title
    s.title = 'Locked while processing'

    // start doing the inputs
    let inputs = f.elements
    for (let i=0; i<inputs.length; i++) {
        // store original state just in case
        inputs[i].dataset.readOnly = inputs[i].readOnly
        inputs[i].setAttribute('readonly', true)
    }

    let spin = get_spinner('light', 'sm')
    s.appendChild(spin)
    s.spinner = spin

    // Create a timeout to unlock the form
    f.locked_timeout = setTimeout(unlock_form, cube_config.api_timeout_delay, s, f)

    return 0;
}


async function put_data(url = "", data = {}) {
    console.log('Uploading to ', url, ':\n\t', data)
    const response = await fetch(url, {
        method: "PUT", 
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
          "Content-Type": "application/json",
        },
        referrerPolicy: "origin", 
        body: JSON.stringify(data), // body data type must match "Content-Type" header
      });
    // TODO: handle errors and stuff better
    return response.json();
}


function api_form_submit(e) {
    // prevent the submission
    e.preventDefault();
    let f = e.srcElement;
    let s = e.submitter
    lock_form(s, f);

    console.log('API form submitted!', e);
    let r = api_form_process(f.elements)
    let ts = new Date().getTime()
    let d = {
        timestamp: ts,
        client: {  // optional meta data about the client
            platform: navigator.platform,
            product: navigator.product,
            version: navigator.productSub,
            vendor: navigator.vendor,
        },
        Query: {  // instructions to the server
            telos: f.dataset.telos,
            techne: f.dataset.techne,
            xenia: f.dataset.xenia,
        },
        Data: r,  // data to upload
    }
    put_data(e.srcElement.action, d).then((data) => {
        console.log(data); // JSON data parsed by `data.json()` call
    });
    console.log(r);
    return 0;
}

/*!
 * This file is part of the CubeRubrics project 
 *
 * Copyright 2023 The Cube Rubrics Authors (https://github.com/CubeRubrics)
 * Licenseed under the GNU Affero GPL (https://raw.githubusercontent.com/CubeRubrics/rprime/main/LICENSE)
 */

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

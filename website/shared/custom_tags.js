// var x_foo = document.registerElement('x-foo')
// document.body.appendChild(new x_foo())

var mega_button = document.registerElement('mega-button', {
    prototype: Object.create(HTMLButtonELement.prototype),
    extends: 'button'
})
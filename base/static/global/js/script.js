const forms = document.querySelectorAll('.form-delete')
forms.forEach((form) => {
	form.addEventListener('submit', (e) => {
		e.preventDefault()
		const confirmed = confirm('Are you sure you want to delete this recipe?')
		if (confirmed) {
			form.submit()
		}
	})
})

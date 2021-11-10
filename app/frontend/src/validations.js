const urlIsValid = url => {
	let parsedUrl
	try {
		parsedUrl = new URL(url)
	} catch (err) {
		return false
	}

	return ['https:', 'http:'].includes(parsedUrl.protocol)
}

export const referenceFormIsValid = (
	firstAuthor,
	year,
	title,
	doi,
	link,
	addErrorMessage
) => {
	let valid = true

	if (firstAuthor !== '') {
		if (firstAuthor.length > 50) {
			addErrorMessage(
				`Ensure the author name is at most 50 characters (name has ${firstAuthor.length} characters)`,
				'firstAuthor'
			)
			valid = false
		}
	}

	if (year !== '') {
		if (year) {
			// 1800 - 2099
			const yearRegex = /^(18|19|20)\d{2}$/

			if (!yearRegex.test(year)) {
				addErrorMessage('Please provide correct year value', 'year')
				valid = false
			}
		}
	}

	if (title === '') {
		addErrorMessage('Please provide the title of the reference', 'title')
		valid = false
	} else {
		if (title.length > 250) {
			addErrorMessage(
				`Ensure the title is at most 250 characters (title has ${title.length} characters)`,
				'title'
			)
			valid = false
		}
	}

	if (doi !== '') {
		if (doi.substring(0, 3) !== '10.') {
			addErrorMessage(
				'Enter the DOI number that begins with 10 followed by a period',
				'doi'
			)
			valid = false
		}
	}

	if (link !== '') {
		urlValidation: {
			if (!urlIsValid(link)) {
				addErrorMessage('Please enter correct url', 'link')
				valid = false
				break urlValidation
			}
			if (link.length > 200) {
				addErrorMessage(
					`Ensure the url is at most 200 characters (url has ${link.length} characters)`,
					'link'
				)
				valid = false
			}
		}
	}

	return valid
}

/* All fields except the title can be null.*/
export const updateRefForSubmission = reference => {
	const updatedReference = { ...reference }
	Object.keys(updatedReference).forEach(k => {
		if (updatedReference[k] === '') {
			updatedReference[k] = null
		}
	})
	updatedReference.year = Number.parseInt(updatedReference.year, 10)
	return updatedReference
}

export const doiFormIsValid = (doi, addErrorMessage) => {
	if (doi === '') {
		addErrorMessage('Please provide the doi number', 'doi')
		return false
	}
	return true
}

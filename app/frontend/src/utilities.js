const idTypes = [
	'name',
	'location',
	'qualifier',
	'structured_name',
	'reference',
	'relation',
	'db_name',
	'db_location',
	'db_qualifier_name',
	'db_qualifier',
	'db_structured_name',
	'db_reference',
]

let ID = 0

export const parseId = id => JSON.parse(id)

export const makeId = (ty, value) => {
	if (!idTypes.includes(ty))
		throw new Error(`Id type must not be one of allowed types, was "${ty}"`)

	const id = value === undefined ? ID++ : Number(value)
	const idString = JSON.stringify({ type: ty, value: id })
	return idString
}

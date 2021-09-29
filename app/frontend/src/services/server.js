const SERVER_DATA = {}

export const initServer = () => {
	const load = (id) => JSON.parse(document.getElementById(id).textContent)
	SERVER_DATA.names = load(`DATA_NAMES`)
	SERVER_DATA.locations =  load(`DATA_LOCATIONS`)
	SERVER_DATA.qualifier_names = load(`DATA_QUALIFIER_NAMES`)
	SERVER_DATA.qualifiers = load(`DATA_QUALIFIERS`)
	SERVER_DATA.structured_names = load(`DATA_STRUCTURED_NAMES`)
	SERVER_DATA.references = load(`DATA_REFERENCES`)
}

export const loadServerData = (k) => k === undefined ? SERVER_DATA : SERVER_DATA[k]
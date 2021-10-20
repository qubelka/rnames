import {
	MAP_VALUE,
	INITIALIZE_MAP_VALUES,
	ADD_NAME,
	UPDATE_NAME,
} from '../action-types'

export const mapId = (key, value) => {
	return {
		type: MAP_VALUE,
		key,
		value,
	}
}

export const initMapvalues = map => {
	return {
		type: INITIALIZE_MAP_VALUES,
		map,
	}
}

export const addName = (refId, name) => {
	return {
		type: ADD_NAME,
		refId,
		name,
	}
}

export const updateName = (refId, name, nameId) => {
	return {
		type: UPDATE_NAME,
		refId,
		name,
		nameId,
	}
}

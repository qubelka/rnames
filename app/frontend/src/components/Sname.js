import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { deleteSname } from '../store/snames/actions'

export const Sname = ({ sname }) => {
	const dispatch = useDispatch()
	const map = useSelector(state => state.map)
	const qualifier_name_id = map[sname.qualifier_id].qualifier_name_id

	const deleteSnameHandler = () => {
		dispatch(deleteSname(sname))
	}

	return (
		<div>
			<p>{map[sname.name_id].name}</p>
			<p>{map[sname.location_id].name}</p>
			<p>{map[qualifier_name_id].name}</p>
			<p>{map[sname.reference_id].title}</p>

			<button type='button' onClick={deleteSnameHandler}>
				Delete
			</button>
		</div>
	)
}

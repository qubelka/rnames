import React from 'react'
import { useSelector } from 'react-redux'

export const Sname = ({ sname }) => {
	const map = useSelector(state => state.map)
	const qualifier_name_id = map[sname.qualifier_id].qualifier_name_id
	return (
		<div>
			<p>{map[sname.name_id].name}</p>
			<p>{map[sname.location_id].name}</p>
			<p>{map[qualifier_name_id].name}</p>
			<p>{map[sname.reference_id].title}</p>
		</div>
	)
}

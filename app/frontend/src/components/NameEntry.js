import React from 'react'
import { useDispatch } from 'react-redux'
import { Dropdown } from './Dropdown'
import { updateName } from '../store/map/actions'
import { makeId, parseId } from '../utilities'

export const NameEntry = ({ id, data }) => {
	const dispatch = useDispatch()
	const name = data.names.find(v => v.id === id)

	const update = ({ target }, field) => {
		const temp = { ...name }
		temp[field] = target.value
		dispatch(updateName(data.id, temp, id))
	}

	const updatevariant = newVariant => {
		const value = parseId(id).value
		const temp = {
			...name,
			id: makeId(newVariant, value),
			variant: newVariant,
		}
		dispatch(updateName(data.id, temp, id))
	}

	const qualifierOptions = [
		['bio', 'Biostratigraphy'],
		['chemo', 'Chemostratigraphy'],
		['chrono', 'Chronostratigraphy'],
		['litho', 'Lithostratigraphy'],
		['region', 'Regional Standard'],
		['seq', 'Sequence-stratigraphy'],
	]

	const levelOptions = [
		[1, '1'],
		[2, '2'],
		[3, '3'],
		[4, '4'],
		[5, '5'],
		[6, '6'],
		[7, '7'],
	]

	const variantOptions = [
		['name', 'Name'],
		['location', 'Location'],
		['qualifier', 'Qualifier'],
	]

	return (
		<div>
			<input
				type='text'
				name='name'
				value={name.name}
				onChange={e => update(e, 'name')}
			/>
			<label htmlFor='variant'>Type:</label>
			<Dropdown
				name='variant'
				onChange={e => updatevariant(e.target.value)}
				options={variantOptions}
				value={name.variant}
			/>
			{name.variant === 'qualifier' ? (
				<>
					<label htmlFor='qualifier'>Qualifier Name:</label>
					<Dropdown
						name='qualifier'
						onChange={e => update(e, 'qualifier')}
						options={qualifierOptions}
						value={name.qualifier}
					/>
					<label htmlFor='level'>Level:</label>
					<Dropdown
						name='level'
						onChange={e => update(e, 'level')}
						options={levelOptions}
						value={name.level}
					/>
				</>
			) : (
				<></>
			)}
		</div>
	)
}

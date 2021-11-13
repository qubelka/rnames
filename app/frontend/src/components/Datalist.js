import React from 'react'

export const Datalist = ({ name, options, value, onChange, id }) => {
	return (
		<>
			<input type='text' list={name} value={value} onChange={onChange} id={id} />
			<datalist id={name}>
				{options.map(tuple => (
					<option key={tuple[0]} value={tuple[1]} />
				))}
			</datalist>
		</>
	)
}

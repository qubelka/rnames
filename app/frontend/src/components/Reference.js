import React from 'react'

export const Reference = ({ reference }) => {
	return (
		<div>
			<p>first_author: {reference.firstAuthor}</p>
			<p>year: {reference.year}</p>
			<p>title: {reference.title}</p>
			<p>doi: {reference.doi}</p>
			<p>link: {reference.link}</p>
		</div>
	)
}

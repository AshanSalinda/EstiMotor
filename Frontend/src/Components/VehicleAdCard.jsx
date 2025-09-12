import React from 'react';

function VehicleAdCard({ ad }) {
    return (
        <div
            className="flex flex-col items-center p-5 cursor-pointer rounded-2xl border border-dark-300 bg-gradient-to-t from-[#000000] to-[#121212] hover:shadow-[0_0_24px_6px_rgba(0,180,255,0.1)] shadow-md transition-transform duration-300 transform hover:scale-[1.03]"
            onClick={() => window.open(ad?.url, '_blank')}
            title={ad.title}
        >
            <img
                src={ad?.image}
                alt={ad?.title}
                className="w-full h-52 object-cover rounded-xl mb-2 border border-dark-300 bg-dark-300"
                onError={(e) => {
                    e.target.src = '/logo.svg';                 // Set the fallback image
                    e.target.classList.remove('object-cover');  // Remove object-cover
                    e.target.classList.add('object-contain');   // Add object-contain
                    e.target.classList.add('p-5');              // Add some padding
                }}
            />
            <div className="flex items-center h-12 my-3">
                <span className="font-semibold text-base text-gray-200 text-center line-clamp-2">{ad?.title}</span>
            </div>
            <div className="text-gray-400 mb-1 text-sm">Year: {ad?.year} | Mileage: {ad?.mileage} km</div>
            <div className="text-gray-400 mb-1 text-sm">Source: {ad?.source}</div>
            <div className="text-primary-450 font-bold text-xl mt-2">Rs. {ad?.price?.toLocaleString()}</div>
        </div>
    );
}

export default VehicleAdCard;

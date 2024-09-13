document.querySelector('#filterForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const homes = document.querySelector('#homes');
    const template = document.querySelector('#homeTemplate');

    const formData = new FormData(e.target);
    const address = formData.get('address');

    // /api/homes/?lat=51.5074&lon=-0.1278&distance=100000&min_price=1000&max_price=5000&balcony=true'
    const params = new URLSearchParams({
        address: formData.get('address'),
        min_price: formData.get('min_price'),
        max_price: formData.get('max_price'),
        surface_area: formData.get('surface_area'),
    });

    const response = await fetch(`/api/homes/?${params}`);
    console.log(await response.text());

    const clone = template.content.cloneNode(true);
    homes.appendChild(clone);
});

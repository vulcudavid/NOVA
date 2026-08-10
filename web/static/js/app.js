const menuButtons = document.querySelectorAll(".menu-button");
const pages = document.querySelectorAll(".page");


menuButtons.forEach(button => {

    button.addEventListener("click", () => {

        const pageName = button.dataset.page;


        // Scoatem active de pe toate butoanele

        menuButtons.forEach(btn => {
            btn.classList.remove("active");
        });


        // Activăm butonul apăsat

        button.classList.add("active");


        // Ascundem toate paginile

        pages.forEach(page => {
            page.classList.remove("active");
        });


        // Afișăm pagina selectată

        const selectedPage =
            document.getElementById(
                `page-${pageName}`
            );

        if (selectedPage) {

            selectedPage.classList.add("active");

        }

    });

});

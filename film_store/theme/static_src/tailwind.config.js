/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            padding: {
                '1.25': '0.3125rem',
            },
            margin: {
                '13': '3.25rem',
                '15': '3.75rem',
                '17': '4.25rem',

                '26': '6.5rem',
            },
            height: {
                '17': '4.25rem',
                '18': '4.5rem',

                '88': '22rem',
            },
            boxShadow: {
                'rim-sm': 'inset 0 1px 0 0 #ffffff0d;',
                'rim-md': 'inset 0 1px 0 0 #ffffff22;',
                'rim-lg': 'inset 0 1px 0 0 #ffffff66;'
            },
            screens: {
                'xxs': '576px'
                // => @media (min-width: 440px) { ... }
            },
            scale: {
                '102': '1.02',
                '107': '1.07',
                
                '180': '1.8',
                '190': '1.9',
                '200': '2',
            },
            colors: {
                'night': {
                    50:  '#ffffff',
                    100: '#999999',
                    200: '#54565c', // Icon/Text disabled color in Card BG
                    300: '#51545d', // 
                    400: '#373a42', // Alt small button in Above Card BG
                    500: '#2d3037', // Alt line in Above Card BG
                    600: '#2f323b', // Above Above Card BG
                    700: '#282b30', // BG of all
                    800: '#242731', // Above Card BG
                    900: '#1f2128', // Card BG
                    950: '#131418', // Darker
                },
                'iris': {
                    500: '#c04cff',
                    600: '#6c5dd3',
                },
                'navy': {
                    500: '#3f8cff',
                    600: '#408dff',
                    700: '#6c83fe',
                },
                'green': {
                    650: '#15883d',
                }
            },
            
            transitionTimingFunction: {
                'in-expo': 'cubic-bezier(0.95, 0.05, 0.795, 0.035)',
                'out-expo': 'cubic-bezier(0.19, 1, 0.22, 1)',
                'out-back-expo': 'cubic-bezier(0.175, 1.885, 0.32, 1.275)',
                'out-back': 'cubic-bezier(0.175, 2.885, 0.32, 1.275)',
                'out-back-little': 'cubic-bezier(0.175, 2.885, 0.32, 1.275)',
            },
        }
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}

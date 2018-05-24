const path = require('path');


module.exports = {
    entry: {
        script: 'script.js'
    },
    resolve: {
        modules: ['desucar/js', 'node_modules']
    },
    output: {
        path: path.resolve('desucar/static'),
        filename: '[name].js?[hash]'
    },
    module: {
        rules: [{
            test: /\.js$/,
            loader: 'babel-loader',
            exclude: /node_modules/,
            options: {
                presets: [
                    ['env', {
                        targets: {
                            browsers: ['> 1%', 'last 2 versions', 'not ie <= 8']
                        }
                    }]
                ],
                plugins: ['transform-decorators-legacy', 'transform-class-properties']
            }
        }]
    }
}
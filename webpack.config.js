module.exports = {
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    devtool: 'eval-source-map',
                    loader: "babel-loader",
                }
            }
        ]
    }
}
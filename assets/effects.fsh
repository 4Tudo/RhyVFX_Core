#version 430


uniform sampler2D tex;
in vec2 uv;
out vec4 out_color;


void main(){
    vec4 tex1 = texture2D(tex,uv).rgba;
    vec4 tex2 = vec4(0.);
    for (float x=-15;x<15;x++){
        for (float y=-15;y<15;y++){
            tex2 += mix(texture2D(tex, vec2(uv.x+x*0.001,uv.y+y*0.001)).rgba,
            texture2D(tex, vec2(uv.x+(x-3)*0.001,uv.y+(y-3)*0.001)).rgba,
            3000
            );
//            tex2 += mix(tex1,
//            texture2D(tex, vec2(uv.x+(x)*0.001,uv.y+(y)*0.001)).rgba,
//            0.1
//            );
        }
    }
    out_color = mix(tex1,tex2,0.001);
//    out_color = tex2;
//    vec2 uv = vec2(0.114,0.514);
//    out_color = vec4(uv,1,1);
}


from direct.showbase.ShowBase import ShowBase
from panda3d.core import PerspectiveLens
from panda3d.core import loadPrcFileData
from panda3d.core import PointLight, Spotlight, AmbientLight
from panda3d.core import Vec3, Vec4, WindowProperties, BamCache
from direct.interval.IntervalGlobal import LerpPosInterval, Parallel
import random
import complexpbr
import sys


class main(ShowBase):
    def __init__(self):
        # load data for self.render first
        loadPrcFileData('', 'window-title Sponza Real-time Demo for Panda3D')
        loadPrcFileData('', 'framebuffer-srgb #t')
        loadPrcFileData('', 'fullscreen #f')
        loadPrcFileData('', 'win-size 1280 720')
        loadPrcFileData('', 'framebuffer-multisample 1')
        loadPrcFileData('', 'multisamples 4')
        # loadPrcFileData('', 'show-frame-rate-meter #t')
        
        super().__init__()
        
        def print_pos():
            print(self.cam.get_pos(self.render))
            
        self.accept('p',print_pos)
        self.accept("escape", sys.exit, [0])
        
        cache = BamCache.get_global_ptr()
        cache.set_cache_models(False)
        cache.set_active(False)
        
        self.sponza_screen_num = 1
        
        def save_screen():
            self.screenshot('sponza_screen_' + str(self.sponza_screen_num))
            self.sponza_screen_num += 1
            
        self.accept('o',save_screen)

        # complexpbr
        complexpbr.apply_shader(self.render, shadow_boost=0.05)
        self.complexpbr_map_z = 0.0
        self.complexpbr_z_tracking = False
        self.cube_buffer.set_sort(-1000)  # ensures the reflections don't lag a frame behind
        
        for x in self.complexpbr_map.find_all_matches('**/+Camera'):
            x.node().get_lens().set_near_far(0.01, 3000)

        def quality_mode():
            complexpbr.screenspace_init()
        
            self.screen_quad.set_shader_input("bloom_intensity", 0.25)
            self.screen_quad.set_shader_input("bloom_threshold", 0.3)
            self.screen_quad.set_shader_input("bloom_blur_width", 20)
            self.screen_quad.set_shader_input("bloom_samples", 1)
            self.screen_quad.set_shader_input('ssr_intensity', 1.0)
            self.screen_quad.set_shader_input('reflection_threshold', 1.6)  # subtracts from intensity
            self.screen_quad.set_shader_input('ssr_step', 5.75)  # helps determine reflect height
            self.screen_quad.set_shader_input('screen_ray_factor', 0.06)  # detail factor
            self.screen_quad.set_shader_input('ssr_samples', 1)  # determines total steps
            self.screen_quad.set_shader_input('ssr_depth_cutoff', 0.52)
            self.screen_quad.set_shader_input('ssr_depth_min', 0.49)
            self.screen_quad.set_shader_input('ssao_samples', 4)
            self.screen_quad.set_shader_input('hsv_r', 1.0)
            self.screen_quad.set_shader_input('hsv_g', 1.05)
            self.screen_quad.set_shader_input('hsv_b', 1.0)
            self.screen_quad.set_shader_input('final_brightness', 1.2)

        # self.accept_once('m', quality_mode)
        quality_mode()
         
        sponza_base = self.loader.load_model('MainSponza_1st_floor.gltf')
        sponza_base.reparent_to(self.render)
        sponza_base.set_pos(0, 0, 0)
        sponza_base.set_scale(1)
        sponza_base.set_shader_input('ao',1.0)
        
        sponza_base = self.loader.load_model('MainSponza_2nd_floor.gltf')
        sponza_base.reparent_to(self.render)
        sponza_base.set_pos(0, 0, 0)
        sponza_base.set_scale(1)
        sponza_base.set_shader_input('ao',1.0)
        
        sponza_base = self.loader.load_model('MainSponza_3rd_floor.gltf')
        sponza_base.reparent_to(self.render)
        sponza_base.set_pos(0, 0, 0)
        sponza_base.set_scale(1)
        sponza_base.set_shader_input('ao',1.0)
        
        curtains_model = self.loader.load_model('NewSponza_Curtains.glb')
        curtains_model.reparent_to(self.render)
        curtains_model.set_pos(0, 0, 0)
        curtains_model.set_scale(1)
        curtains_model.set_two_sided(False)
        curtains_model.set_shader_input('ao',1.0)

        cypress_model = self.loader.load_model('NewSponza_CypressTree_BK_SM.glb')
        cypress_model.reparent_to(self.render)
        cypress_model.set_pos(-3, 0, 0)
        cypress_model.set_scale(1)
        cypress_model.set_two_sided(False)
        cypress_model.set_shader_input('ao',1.0)
        
        cypress_model = self.loader.load_model('NewSponza_CypressTree_LF.glb')
        cypress_model.reparent_to(self.render)
        cypress_model.set_pos(-3, 0, 0)
        cypress_model.set_scale(1)
        cypress_model.set_two_sided(False)
        cypress_model.set_shader_input('ao',1.0)
        
        amb_light = AmbientLight('amblight')
        amb_light.set_color((1,1,1.2,1))
        amb_light_node = self.render.attach_new_node(amb_light)
        self.render.set_light(amb_light_node)
        
        point_ambient_1 = PointLight('point_ambient_1')
        point_ambient_1.set_color(Vec4(Vec3(1.5),1))
        point_ambient_1 = self.render.attach_new_node(point_ambient_1)
        point_ambient_1.set_pos(0,0,2)
        self.render.set_light(point_ambient_1)
        
        env_light_1 = PointLight('env_light_1')
        env_light_1.set_color(Vec4(Vec3(6),1))
        env_light_1 = self.render.attach_new_node(env_light_1)
        env_light_1.set_pos(0,0,0)
        base_env = loader.load_model('daytime_skybox.gltf')
        base_env.name = 'basic_skybox'
        base_env.reparent_to(self.render)
        base_env.set_scale(1)
        base_env.set_pos(0,0,0)
        base_env.set_light(env_light_1)

        spotlight_1 = Spotlight('spotlight_1')
        spotlight_1.set_color((15,15,10,1))
        # spotlight_1.set_color((10,10,10,1))
        spotlight_1.set_shadow_caster(True, 16384, 16384)
        lens = PerspectiveLens()
        lens.set_fov(85)
        spotlight_1.set_lens(lens)
        spotlight_1_node = self.render.attach_new_node(spotlight_1)
        # illuminate lion bust
        spotlight_1_node.set_pos(10, -5, 40)
        spotlight_1_node.look_at(0,5,0)
        self.render.set_light(spotlight_1_node)
        base_env.set_light_off(spotlight_1_node)
        
        spotlight_2 = Spotlight('spotlight_2')
        spotlight_2.set_color((1,1,0.75,1))
        # spotlight_2.set_shadow_caster(True, 8096, 8096)
        lens = PerspectiveLens()
        lens.set_fov(85)
        spotlight_2.set_lens(lens)
        spotlight_2_node = self.render.attach_new_node(spotlight_2)
        # illuminate lion bust
        spotlight_2_node.set_pos(10, 5, 40)
        spotlight_2_node.look_at(0,-5,0)
        self.render.set_light(spotlight_2_node)
        base_env.set_light_off(spotlight_2_node)
        
        # look at lion bust
        self.cam_look_pos = Vec3(-10,0,5.5)
        self.cam.set_pos(8.0,0,1.0)  # bottom to top
        # self.cam.set_pos(-3.0,0,20)  # top to bottom
        self.camLens.set_fov(120)
        self.cam.look_at(self.cam_look_pos)
        complexpbr.set_cubebuff_inactive()
        
        # optionally animate the sun
        i = LerpPosInterval(spotlight_1_node, 200, Vec3(10,5,40))
        i_2 = LerpPosInterval(spotlight_2_node, 200, Vec3(10,-5,40))
        par = Parallel()
        par.append(i)
        par.append(i_2)
        # par.start()  # enable animation by uncommenting this line
         
        def bottom_to_top(Task):        
            dt = self.clock.get_dt()
            cam_pos = self.cam.get_pos()
            speed = 5
            
            if self.cam.get_z() < 20:
                self.cam.set_pos(cam_pos[0] - 0.01 * speed * dt,cam_pos[1],cam_pos[2] + 0.02 * speed * dt)
                self.cam.look_at(self.cam_look_pos)
             
            return Task.cont
        
        self.taskMgr.add(bottom_to_top)

         
app = main()
app.run()
